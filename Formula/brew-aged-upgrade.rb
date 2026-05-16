# typed: false
# frozen_string_literal: true

class BrewAgedUpgrade < Formula
  desc "Upgrade Homebrew packages only after their formula is N days old"
  homepage "https://github.com/nhm7/homebrew-aged-upgrade"
  head "https://github.com/nhm7/homebrew-aged-upgrade.git", branch: "main"
  license "MIT"

  depends_on "python3"

  def install
    libexec.install "libexec/brew-aged-upgrade"
    bin.write_exec_script libexec/"brew-aged-upgrade"
  end

  test do
    assert_predicate bin/"brew-aged-upgrade", :exist?
  end
end
