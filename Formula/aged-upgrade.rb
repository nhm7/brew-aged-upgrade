# typed: false
# frozen_string_literal: true

class AgedUpgrade < Formula
  desc "Upgrade Homebrew packages only after they have been outdated for N days"
  homepage "https://github.com/nhm7/homebrew-aged-upgrade"
  url "https://github.com/nhm7/homebrew-aged-upgrade/archive/refs/tags/v1.2.0.tar.gz"
  sha256 "ab63e99d6a791d97e56083ea79f666f70fa1f7f15adf03d8860d7b9a621ff558"

  head "https://github.com/nhm7/homebrew-aged-upgrade.git", branch: "main"
  license "MIT"

  depends_on :macos
  uses_from_macos "python3"

  def install
    libexec.install "libexec/brew-aged-upgrade", "libexec/brew-aged-upgrade-core.py"
    bin.write_exec_script libexec/"brew-aged-upgrade"
  end

  def caveats
    <<~EOS
      The CLI is installed as `brew-aged-upgrade`, not `aged-upgrade`.

      To enable daily auto-upgrade:
        brew-aged-upgrade start
    EOS
  end

  test do
    output = shell_output("#{bin}/brew-aged-upgrade help")
    assert_match "start", output
    assert_match "stop", output
    assert_match "status", output
  end
end
